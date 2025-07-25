from fastapi import FastAPI
from app.products import routes as product_routes
from app.categories import routes as category_routes
from app.orders import routes as order_routes
from app.users.admin import routes as admin_routes
from app.users.customers import routes as customer_routes
from app.auth.routes import router as auth_router
from fastapi_pagination import add_pagination
app = FastAPI(title="ECommerce API")
add_pagination(app)
app.include_router(product_routes.router)
app.include_router(category_routes.router)
app.include_router(order_routes.router)
app.include_router(admin_routes.router)
app.include_router(customer_routes.router)
app.include_router(auth_router)
