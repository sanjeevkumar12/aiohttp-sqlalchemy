from application.extensions import db

from .models import Poll


class BaseService(object):
    def __init__(self, session=None):
        self.session = session

    def set_session(self, session):
        self.session = session
        return self

    async def execute_select(self, stmt):
        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()


class PollService(BaseService):
    async def list_all(self):
        async with self.session() as session:
            result = await session.execute(db.select(Poll))
            return result.scalars().all()

    async def create_poll(self, label):
        async with self.session() as session:
            async with session.begin():
                poll = Poll(label=label)
                session.add(poll)
                session.flush()
                return poll


poll_service = PollService()
