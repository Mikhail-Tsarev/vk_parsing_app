import sqlalchemy

from main import db


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey("domain.owner_id"))
    date = db.Column(db.Integer)
    text = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    reposts = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"{self.id} {self.text}"


class Attachment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    attachment_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey("domain.owner_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    type = db.Column(db.String)
    url = db.Column(db.String)


class Domain(db.Model):

    owner_id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String)

    def __repr__(self):
        return f"{self.owner_id} {self.domain}"


def save_post_in_db(data):
    if not Post.query.filter_by(
        post_id=data["id"], owner_id=data["owner_id"]
    ).first():
        post_record = Post(
            post_id=data["id"],
            owner_id=data["owner_id"],
            date=data["date"],
            text=data["text"],
            likes=data["likes"]["count"],
            reposts=data["reposts"]["count"],
            comments=data["comments"]["count"],
        )
        db.session.add(post_record)
        db.session.commit()
        return True


def save_attachments_in_db(data):

    if "attachments" in data.keys():

        for attachment in data["attachments"]:
            if attachment["type"] == "link":
                attachment_id = ""
                url = attachment["link"]["url"]

            elif attachment["type"] == "sticker":
                attachment_id = attachment["sticker"]["sticker_id"]
                url = ""
            else:
                attachment_id = attachment[attachment["type"]]["id"]
                url = f'https://vk.com/{attachment["type"]}{attachment[attachment["type"]]["owner_id"]}_{attachment_id}'

            if attachment["type"] in (
                "link",
                "app",
                "pretty_cards",
                "event",
            ):
                owner_id = ""
            else:
                owner_id = attachment[attachment["type"]]["owner_id"]

            attachment_record = Attachment(
                attachment_id=attachment_id,
                owner_id=owner_id,
                type=attachment["type"],
                post_id=data["id"],
                url=url,
            )
            db.session.add(attachment_record)
        db.session.commit()


def save_domain_in_db(data, domain):
    domain_record = Domain(owner_id=data["owner_id"], domain=domain)
    try:
        db.session.add(domain_record)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.close()

    return True
