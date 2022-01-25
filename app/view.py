from flask import redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import app
from forms import QueryForm
from funcs import get_all_posts, get_domain, get_unix_time
from vk_token import token


@app.route("/", methods=["GET", "POST"])
def index():
    form = QueryForm()
    if form.validate_on_submit():

        year = form.year.data
        month = form.month.data
        day = form.day.data
        link = get_domain(form.link.data)
        date = "-".join((year, month, day))

        return redirect(
            url_for(
                "result",
                date=date,
                link=link,
            )
        )
    return render_template("index.html", form=form)


# @app.route("/result", methods=["GET"])
# def result():
#     if "link" not in request.args.keys():
#         return redirect(url_for("index"))
#     link = request.args["link"]
#     date = get_unix_time(request.args["date"])
#     posts = get_all_posts(link, token, date)
#     res = ""
#     cnt = 1
#     for post in posts:
#         res += str(cnt) + "---" + post["text"] + "<br>"
#         cnt += 1
#     return render_template(
#         "result.html", date=request.args["date"], link=link, res=res
#     )
