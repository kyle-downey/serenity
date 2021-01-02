import yfinance

from serenity.db.api import connect_serenity_db


def backfill_symbol(cur, symbol):
    ticker = yfinance.Ticker(symbol)
    marks = ticker.history(period="max")

    cur.execute("SELECT instrument_id FROM serenity.instrument WHERE instrument_code = %s", (symbol,))
    instrument_id = cur.fetchone()[0]

    cur.execute("SELECT mark_type_id FROM serenity.mark_type WHERE mark_type_code = %s", ("YahooDailyClose",))
    mark_type_id = cur.fetchone()[0]

    for index, row in marks.iterrows():
        cur.execute("INSERT INTO serenity.instrument_mark (instrument_id, mark_type_id, mark_time, mark) "
                    "VALUES (%s, %s, %s, %s)", (instrument_id, mark_type_id, index, float(row['Close'])))

    conn.commit()


if __name__ == '__main__':
    conn = connect_serenity_db()
    cur = conn.cursor()

    backfill_symbol(cur, "BTC-USD")
    backfill_symbol(cur, "ETH-USD")
    backfill_symbol(cur, "ZEC-USD")
