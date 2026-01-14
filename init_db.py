"""Database initialization script."""
from app import create_app
from models import db, User, StoreItem
from datetime import datetime

def init_database():
    """Initialize database with tables and sample data."""
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")
        
        # Check if we need to add sample data
        if User.query.count() == 0:
            print("\nAdding sample data...")
            
            # Create sample users
            collector1 = User(
                email='collector1@example.com',
                username='collector1',
                user_type='collector',
                full_name='John Collector',
                phone='1234567890',
                address='123 Green Street',
                latitude=13.0827,
                longitude=80.2707,
                points=0
            )
            collector1.set_password('password123')
            
            collector2 = User(
                email='collector2@example.com',
                username='collector2',
                user_type='collector',
                full_name='Jane Recycler',
                phone='0987654321',
                address='456 Eco Avenue',
                latitude=13.0878,
                longitude=80.2785,
                points=0
            )
            collector2.set_password('password123')
            
            seeker1 = User(
                email='seeker1@example.com',
                username='seeker1',
                user_type='seeker',
                full_name='Mike Reporter',
                phone='5551234567',
                address='789 Clean Road',
                latitude=13.0900,
                longitude=80.2800,
                points=0
            )
            seeker1.set_password('password123')
            
            db.session.add_all([collector1, collector2, seeker1])
            print("✓ Sample users created")
            
            # Create sample store items
            items = [
                StoreItem(
                    name='$5 Amazon Gift Card',
                    description='Redeem for a $5 Amazon gift card',
                    category='voucher',
                    points_cost=500,
                    stock=100,
                    is_active=True
                ),
                StoreItem(
                    name='$10 Amazon Gift Card',
                    description='Redeem for a $10 Amazon gift card',
                    category='voucher',
                    points_cost=1000,
                    stock=50,
                    is_active=True
                ),
                StoreItem(
                    name='Reusable Water Bottle',
                    description='Eco-friendly stainless steel water bottle',
                    category='product',
                    points_cost=300,
                    stock=30,
                    is_active=True
                ),
                StoreItem(
                    name='Recycled Tote Bag',
                    description='Stylish tote bag made from recycled materials',
                    category='product',
                    points_cost=200,
                    stock=50,
                    is_active=True
                ),
                StoreItem(
                    name='Plant a Tree',
                    description='We will plant a tree in your name',
                    category='donation',
                    points_cost=150,
                    stock=1000,
                    is_active=True
                ),
                StoreItem(
                    name='Ocean Cleanup Donation',
                    description='Support ocean cleanup initiatives',
                    category='donation',
                    points_cost=250,
                    stock=1000,
                    is_active=True
                )
            ]
            
            db.session.add_all(items)
            print("✓ Sample store items created")
            
            # Commit all changes
            db.session.commit()
            print("\n✓ Database initialized successfully!")
            
            print("\n" + "="*50)
            print("Sample Login Credentials:")
            print("="*50)
            print("Collector 1:")
            print("  Username: collector1")
            print("  Password: password123")
            print("\nCollector 2:")
            print("  Username: collector2")
            print("  Password: password123")
            print("\nSeeker 1:")
            print("  Username: seeker1")
            print("  Password: password123")
            print("="*50)
        else:
            print("\n✓ Database already contains data")

if __name__ == '__main__':
    init_database()