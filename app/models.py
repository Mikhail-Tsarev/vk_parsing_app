from app import db


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("domain.owner_id"))
    date = db.Column(db.Integer)
    text = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    reposts = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"{self.id} {self.text}"


class Attachment(db.model):

    id = db.Column(db.Integer, primary_key=True)
    attachment_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey("domain.owner_id"))
    type = db.Column(db.String)


class Domain(db.Model):

    owner_id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String)

    def __repr__(self):
        return f"{self.owner_id} {self.domain}"


def main():
    """
    Function creates all  tables.
    """
    db.create_all()


if __name__ == "__main__":
    main()
