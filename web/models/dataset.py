from web import db


class Dataset(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(10), nullable=False)
    model = db.Column(db.String(10), nullable=False)
    activity_name = db.Column(db.String(200), nullable=False)
    geography_name = db.Column(db.String(50), nullable=False)
    reference_product_name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Dataset({self.version},{self.model},{self.activity_name},\
        {self.geography_name},{self.reference_product_name},{self.user_id})'
