import sqlite3
from flask import Flask, render_template

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)

class_active = "active"


class Database:
    @staticmethod
    def query(
        db: str, sql: str, args: tuple, many: bool = True
    ) -> list[tuple] or tuple:
        try:
            with sqlite3.connect(db) as connection:
                cursor = connection.cursor()
                cursor.execute(sql, args)
                if many:
                    return cursor.fetchall()
                return cursor.fetchone()
        except Exception as error:
            print(error)

    @staticmethod
    def select(
        db: str, table: str, columns: list[str], id: int = None
    ) -> list[tuple] or tuple:
        query = "SELECT {} FROM {}".format(", ".join(columns), table)
        if not id:
            return Database.query(db=db, sql=query, args=())
        return Database.query(
            sql=f"{query} WHERE id =?",
            args=(id,),
            many=False,
        )

    @staticmethod
    def insert(
        db: str, table: str, columns: list[str], values: list[any]
    ) -> list[tuple]:
        return Database.query(
            db=db,
            sql="INSERT INTO {} ({}) VALUES ({})".format(
                table, ", ".join(columns), ", ".join(["?" for _ in values])
            ),
            args=values,
        )


class Views:
    class Base:
        @staticmethod
        @app.route("/")
        def home():
            home_active = class_active
            return render_template("home.html", home_active=home_active)

        @staticmethod
        @app.route("/about")
        def about():
            about_active = class_active
            doctors = Database.select(
                db="database/doctors.db",
                table="doctors",
                columns=["name", "description"],
            )
            return render_template(
                "about.html", about_active=about_active, doctors=doctors
            )

        @staticmethod
        @app.route("/pricing")
        def pricing():
            pricing = Database.select(
                db="database/pricing.db",
                table="pricing",
                columns=["name", "description", "price"],
            )
            pricing_active = class_active
            return render_template(
                "pricing.html", pricing_active=pricing_active, pricing=pricing
            )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
