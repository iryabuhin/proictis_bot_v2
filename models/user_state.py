from tortoise import Model, fields
from vkbottle.branch import DatabaseBranch
import typing


class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    time = fields.IntField()

    class Meta:
        database = 'user'


class UserState(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    branch = fields.CharField(32)
    context = fields.JSONField()

    class Meta:
        database = "user_state"


class DBStoredBranch(DatabaseBranch):
    async def get_user(self, uid: int) -> typing.Tuple[str, typing.Union[str, dict]]:
        u = await UserState.get(uid=uid)
        return u.branch, u.context

    async def set_user(self, uid: int, branch: str, context: str) -> None:
        u = await UserState.get_or_none(uid=uid)
        if u is None:
            await UserState.create(uid=uid, branch=branch, context=context)
        else:
            u.branch = branch
            u.context = context
            return await u.save()


    async def delete_user(self, uid: int):
        u = await UserState.get(uid=uid)
        await u.delete()

    async def all_users(self) -> typing.List[int]:
        return [u.uid async for u in UserState.all()]
