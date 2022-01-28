import csv
import time
from functools import lru_cache
from io import StringIO

import vk_api
import vk_api.exceptions
from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from config import TOKEN
from forms import GetCsv, QueryForm
from main import app, db
from models import (
    Attachment,
    Domain,
    Post,
    save_attachments_in_db,
    save_domain_in_db,
    save_post_in_db,
)
from utils import get_domain, get_unix_time


@lru_cache()
def get_all_posts(domain: str, token: str, date) -> None:

    offset = 0
    flag = True
    domain_flag = True
    while flag:
        session = vk_api.VkApi(token=token)
        vk = session.get_api()
        response = vk.wall.get(domain=domain, count=100, offset=offset)

        if len(response) == 0:
            flag = False
        if domain_flag:
            save_domain_in_db(response["items"][0], domain)
            exit_post = response["items"][0]
            domain_flag = False
        if len(response["items"]) == 0:
            break
        for item in response["items"]:
            if item["date"] < date and item is not exit_post:
                flag = False
                break
            new = save_post_in_db(item)
            if new:
                save_attachments_in_db(item)

        offset += 100
        time.sleep(0.2)


def get_post_data(link, date, fields):
    return (
        db.session.query(*fields)
        .join(Domain, Post.owner_id == Domain.owner_id)
        .where(Domain.domain == link)
        .filter(Post.date >= date)
        .all()
    )


def get_attachments(post_id):
    return (
        db.session.query(Attachment.url)
        .where(Attachment.post_id == post_id)
        .all()
    )


db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    form = QueryForm()
    if form.validate_on_submit():

        year = form.year.data
        month = form.month.data
        day = form.day.data
        link = get_domain(form.link.data)
        date = "-".join((year, month, day))
        unix_date = get_unix_time(date)
        id = int(form.id.data)
        text = int(form.text.data)
        attachments = int(form.attachments.data)
        links = int(form.links.data)
        likes = int(form.likes.data)
        reposts = int(form.reposts.data)
        comments = int(form.reposts.data)

        return redirect(
            url_for(
                "result",
                date=date,
                link=link,
                unix_date=unix_date,
                id=id,
                text=text,
                attachments=attachments,
                links=links,
                likes=likes,
                reposts=reposts,
                comments=comments,
            )
        )

    return render_template("index.html", form=form)


@app.route("/result", methods=["GET", "POST"])
def result():
    form1 = GetCsv()

    if "link" not in request.args.keys():
        return redirect(url_for("index"))

    link = request.args["link"]
    unix_date = int(request.args["unix_date"])
    date = request.args["date"]
    id = request.args["id"]
    text = request.args["text"]
    attachments = request.args["attachments"]
    links = request.args["links"]
    likes = request.args["likes"]
    reposts = request.args["reposts"]
    comments = request.args["comments"]

    if unix_date == 0:
        flash("ОШИБКА: Некорректное сочетание дня и месяца.")
        return redirect(url_for("index"))

    try:
        get_all_posts(link, TOKEN, unix_date)
    except vk_api.exceptions.ApiError as err:

        if err.error["error_code"] == 30:
            flash(
                f"ОШИБКА: Данный профиль закрыт настройками приватности.\nПопробуйте ввести адрес другой страницы."
            )
        else:
            print(err.error["error_code"], err.error["error_msg"])
            flash(f'{err.error["error_code"]}, {err.error["error_msg"]}')
        return redirect(url_for("index"))
    posts_collected = len(get_post_data(link, unix_date, [Post.id]))
    if form1.validate_on_submit():
        return get_csv()

    return render_template(
        "result.html",
        date=date,
        unix_date=unix_date,
        link=link,
        form1=form1,
        id=id,
        text=text,
        attachments=attachments,
        links=links,
        likes=likes,
        reposts=reposts,
        comments=comments,
        posts_collected=posts_collected,
    )


@app.route("/get_csv", methods=["POST"])
def get_csv():

    link = request.args["link"]
    date = request.args["date"]
    unix_date = request.args["unix_date"]
    id = int(request.args["id"])
    text = int(request.args["text"])
    number_of_attachments = int(request.args["attachments"])
    links = int(request.args["links"])
    likes = int(request.args["likes"])
    reposts = int(request.args["reposts"])
    comments = int(request.args["comments"])

    chosen_fields = [Post.post_id]

    if text:
        chosen_fields.append(Post.text)
    if likes:
        chosen_fields.append(Post.likes)
    if reposts:
        chosen_fields.append(Post.reposts)
    if comments:
        chosen_fields.append(Post.comments)

    data = get_post_data(link, unix_date, chosen_fields)
    content = []
    for el in data:
        row = []
        if id:
            row.extend([str(field) for field in el])
        else:
            row.extend([str(field) for field in el[1:]])
        attachments = [x.url for x in get_attachments(el.post_id)]
        if number_of_attachments:
            row.append(str(len(attachments)))
        if len(attachments) > 0:
            if links:
                row.extend([str(link) for link in attachments])

        content.append(row)

    si = StringIO()
    cw = csv.writer(si, delimiter=";")
    cw.writerows(content)
    output = make_response(si.getvalue())
    output.headers[
        "Content-Disposition"
    ] = f"attachment; filename={link}-{date}.csv"
    output.headers["Content-type"] = "text/csv"
    return output
