from CTFd.models import db, Challenges, Users


class GoCQHttpDB(db.Model):
    __tablename__ = "GoCQHttpDB"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    groupid = db.Column(db.Text)
    goauth = db.Column(db.Text)
    feishuid = db.Column(db.Text)
    robotstatus = db.Column(db.Text)

    def __init__(self, address, groupid, goauth, feishuid, robotstatus):
        self.address = address
        self.groupid = groupid
        self.goauth = goauth
        self.feishuid = feishuid
        self.robotstatus = robotstatus


def view_go_cq_http_config():
    godb = db.session.query(GoCQHttpDB).all()
    if len(godb) == 0:
        return False
    else:
        for item in godb:
            return {"address": item.address, "groupid": item.groupid, "goauth": item.goauth, "feishuid": item.feishuid, "robotstatus": item.robotstatus}


def update_go_cq_http_config(address, groupid, goauth, feishuid, robotstatus):
    godb = db.session.query(GoCQHttpDB).filter(GoCQHttpDB.id==1).update({"address": address, "groupid": groupid, "goauth": goauth, "feishuid": feishuid, "robotstatus": robotstatus})
    db.session.commit()

def add_go_cq_http_config(address, groupid, goauth, feishuid, robotstatus):
    if view_go_cq_http_config():
        return False
    else:
        godb = GoCQHttpDB(address, groupid, goauth, feishuid, robotstatus)
        db.session.add(godb)
        db.session.commit()