from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cat import Cat
from app.schemas.cat import (
    CatCreate,
    CatResponse,
    CatAllResponse,
    UpdateCatRequest,
    UpdateCatResponse,
    DeleteCatResponse,
)
from app.utils.logging import logger


class CatService:
    @staticmethod
    async def create_cat(db: AsyncSession, cat_data: CatCreate) -> CatResponse:
        """猫を作成する"""
        try:
            new_cat = Cat(**cat_data.model_dump())
            db.add(new_cat)
            await db.commit()
            await db.refresh(new_cat)

            logger.info(f"猫を作成しました: {new_cat.id}")
            return CatResponse.model_validate(new_cat)
        except Exception as e:
            await db.rollback()
            logger.error(f"猫の作成中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def get_all_cats(db: AsyncSession) -> CatAllResponse:
        """すべての猫を取得する"""
        try:
            result = await db.execute(select(Cat))
            cats = result.scalars().all()

            cat_responses = [CatResponse.model_validate(cat) for cat in cats]
            logger.info(f"{len(cat_responses)}匹の猫を取得しました")

            return CatAllResponse(cats=cat_responses)
        except Exception as e:
            logger.error(f"猫の取得中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def get_cat_by_id(db: AsyncSession, cat_id: str) -> CatResponse:
        """IDで猫を取得する"""
        try:
            result = await db.execute(select(Cat).where(Cat.id == cat_id))
            cat = result.scalar_one_or_none()

            if not cat:
                raise ValueError(f"ID {cat_id} の猫が見つかりません")

            return CatResponse.model_validate(cat)
        except Exception as e:
            logger.error(f"猫の取得中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def update_cat(
        cat_id: str, update_data: UpdateCatRequest, db: AsyncSession
    ) -> UpdateCatResponse:
        """猫の情報を更新する"""
        try:
            result = await db.execute(select(Cat).where(Cat.id == cat_id))
            cat = result.scalar_one_or_none()

            if not cat:
                raise ValueError(f"ID {cat_id} の猫が見つかりません")

            # 更新データを適用
            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(cat, field, value)

            await db.commit()
            await db.refresh(cat)

            logger.info(f"猫を更新しました: {cat_id}")
            return UpdateCatResponse.model_validate(cat)
        except Exception as e:
            await db.rollback()
            logger.error(f"猫の更新中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def delete_cat(cat_id: str, db: AsyncSession) -> DeleteCatResponse:
        """猫を削除する"""
        try:
            result = await db.execute(select(Cat).where(Cat.id == cat_id))
            cat = result.scalar_one_or_none()

            if not cat:
                raise ValueError(f"ID {cat_id} の猫が見つかりません")

            await db.delete(cat)
            await db.commit()

            logger.info(f"猫を削除しました: {cat_id}")
            return DeleteCatResponse(message="猫を正常に削除しました", id=cat_id)
        except Exception as e:
            await db.rollback()
            logger.error(f"猫の削除中にエラーが発生しました: {str(e)}")
            raise e
