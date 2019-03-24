#!/usr/bin/env python

from database_setup import Category, CategoryItem, User
from engine import Engine

def main():
    try:
        DATABASE = 'postgresql://linux:linux@127.0.0.1:5432/catalog'
        engine = Engine(DATABASE)
        session = engine.get_session()

        print("[INFO] Started...")
        # Create New User
        user = User(
            name="demo",
            email="demo@example.com",
            photo="demo-photo.png"
        )
        session.add(user)
        session.flush()

        # Dairy Products and its products
        c1 = Category(
            title="Dairy Products",
            user_id=user.id
        )
        session.add(c1)
        session.flush()

        c1_item1 = CategoryItem(
            title="Cheese",
            description="Cheese",
            category_id=c1.id
        )
        c1_item2 = CategoryItem(
            title="Butter",
            description="Butter",
            category_id=c1.id
        )
        c1_item3 = CategoryItem(
            title="Ice Cream",
            description="Ice Cream",
            category_id=c1.id
        )
        c1_item4 = CategoryItem(
            title="Ice Milk",
            description="Ice Milk",
            category_id=c1.id
        )
        session.add(c1_item1)
        session.add(c1_item2)
        session.add(c1_item3)
        session.add(c1_item4)


        # Red Meat and its relative
        c2 = Category(
            title="Red Meat",
            user_id=user.id
        )
        session.add(c2)
        session.flush()

        c2_item1 = CategoryItem(
            title="Beef",
            description="Beef",
            category_id=c2.id
        )
        c2_item2 = CategoryItem(
            title="Pork",
            description="Pork",
            category_id=c2.id
        )
        c2_item3 = CategoryItem(
            title="Goat",
            description="Goat",
            category_id=c2.id
        )
        c2_item4 = CategoryItem(
            title="Veal",
            description="Veal",
            category_id=c2.id
        )
        session.add(c2_item1)
        session.add(c2_item2)
        session.add(c2_item3)
        session.add(c2_item4)


        # White Meat and it relative
        c3 = Category(
            title="White Meat",
            user_id=user.id
        )
        session.add(c3)
        session.flush()

        c3_item1 = CategoryItem(
            title="Chicken",
            description="Chicken",
            category_id=c3.id
        )
        c3_item2 = CategoryItem(
            title="Fish",
            description="Fish",
            category_id=c3.id
        )
        session.add(c3_item1)
        session.add(c3_item2)

        # Vegetable and its relative
        c4 = Category(
            title="Vegetable",
            user_id=user.id
        )
        session.add(c4)
        session.flush()

        c4_item1 = CategoryItem(
            title="Artichoke",
            description="Artichoke",
            category_id=c4.id
        )
        c4_item2 = CategoryItem(
            title="Broccoli",
            description="Broccoli ",
            category_id=c4.id
        )
        c4_item3 = CategoryItem(
            title="Frisee",
            description="Frisee",
            category_id=c4.id
        )
        c4_item4 = CategoryItem(
            title="Carot",
            description="Carot",
            category_id=c4.id
        )
        session.add(c4_item1)
        session.add(c4_item2)
        session.add(c4_item3)
        session.add(c4_item4)

        session.commit()
        print("[Info] Done")
    except Exception as e:
        print("[Error] Database Initial", e)


if __name__ == "__main__":
    main()