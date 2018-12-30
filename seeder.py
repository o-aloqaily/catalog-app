from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

Category1 = Category(title="Soccer")
Category2 = Category(title="Basketball")
Category3 = Category(title="Baseball")
Category4 = Category(title="Frisbee")
Category5 = Category(title="Snowboarding")
Category6 = Category(title="Rock Climbing")
Category7 = Category(title="Foosball")
Category8 = Category(title="Skating")
Category9 = Category(title="Hockey")

user = User(name="Osama Aloqaily", email="osamaoqaily@gmail.com")

item1 = Item(title="Soccer Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="1")
item3 = Item(title="Basketball Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="2")
item4 = Item(title="Baseball Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="3")
item5 = Item(title="Frisbee Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="4")
item6 = Item(title="Snowboarding Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="5")
item7 = Item(title="Rock Climbing Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="6")
item8 = Item(title="Foosball Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="7")
item9 = Item(title="Skating Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="8")
item10 = Item(title="Hockey Item", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin tristique mi a purus volutpat ultricies. Vivamus id consequat urna. Curabitur tincidunt sodales ornare. Nam consectetur augue sed feugiat consectetur. Nam nec urna dapibus, condimentum nisl nec, fermentum sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras tincidunt urna vel tortor porta aliquam. Vestibulum et diam sapien. Praesent egestas ante a porta accumsan. Aenean sed sapien in nisi sollicitudin vestibulum. Morbi eget blandit turpis. Maecenas id scelerisque libero. Donec eget lacinia lacus, vitae suscipit ipsum.", 
                user_id="1", category_id="9")

session.add_all([item1, item3, item4, item5, item6, item7, item8, item9, item10])
session.add_all([Category1, Category2, Category3, Category4, Category5, Category6, Category7, Category8, Category9])
session.commit()

