from google_play_scraper import reviews, Sort
import pandas as pd
import psycopg2
import time

def extract(app_id, total_reviews=10000):
    all_reviews = []
    continuation_token = None

    while len(all_reviews) < total_reviews:
        result, continuation_token = reviews(
            app_id,
            lang="id",
            country="id",
            sort=Sort.NEWEST,
            count=100,
            continuation_token=continuation_token
        )

        all_reviews.extend(result)
        print("Total terkumpul:", len(all_reviews))

        if continuation_token is None:
            break

    return all_reviews[:total_reviews]

def transform(data):
    df = pd.DataFrame(data)

    df["review_datetime"] = df["at"]
    df["timestamp_unix"] = df["review_datetime"].apply(
        lambda x: int(time.mktime(x.timetuple()))
    )
    df["timestamp_formatted"] = df["review_datetime"].apply(
        lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
    )

    final_df = df[
        [
            "reviewId",
            "userName",
            "userImage",
            "content",
            "score",
            "thumbsUpCount",
            "reviewCreatedVersion",
            "review_datetime",
            "replyContent",
            "repliedAt",
            "appVersion",
            "timestamp_unix",
            "timestamp_formatted"
        ]
    ]

    final_df = final_df.replace({pd.NaT: None})
    final_df = final_df.where(pd.notnull(final_df), None)

    return final_df

def load_to_postgres(df):
    conn = psycopg2.connect(
        host="localhost",
        database="dana_etl",
        user="postgres",
        password="0000"
    )
    
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO dana_reviews VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            tuple(row)
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Data berhasil masuk ke PostgreSQL")

if __name__ == "__main__":
    app_id = "id.dana"

    print("Mulai Extract")
    raw_data = extract(app_id)

    print("Mulai Transform")
    final_data = transform(raw_data)

    print("Mulai Load")
    load_to_postgres(final_data)

    print("ETL selesai")