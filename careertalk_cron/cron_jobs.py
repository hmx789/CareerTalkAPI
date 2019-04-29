from sqlalchemy import func

from careertalk.models import db, Like, Top5
from careertalk import create_operation
from common.config import Config


# Todo later we need top5 config and then make this better.
def calculate_top5():
    config = Config()
    app = create_operation(config, "Calculate Top 5")
    db.init_app(app)

    with app.app_context():
        session = db.session
        fair_id = 1

        top_5_to_delete = Top5.query.filter_by(careerfair_id=fair_id).all()
        if top_5_to_delete:
            session.delete(top_5_to_delete)
            session.commit()

        employers = session.query(Like.employer_id, func.count(Like.employer_id).label('count')).filter_by(
            careerfair_id=fair_id).group_by(Like.employer_id).order_by(
            func.count(Like.employer_id).label('count').desc()).limit(5)

        top5_employers = []
        for e in employers:
            top5_employers.append(e[0])

        if len(top5_employers) < 5:
            return None

        top5 = Top5(top1=top5_employers[0], top2=top5_employers[1], top3=top5_employers[2], top4=top5_employers[3],
                    top5=top5_employers[4], careerfair_id=fair_id)

        session.add(top5)
        session.commit()

    return top5_employers
