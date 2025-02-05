# from api.controllers.market_controllers import router as MarketRouter

from api.controllers import market, rules, alerts


def init_routes(app):
    app.include_router(market.router)
    app.include_router(rules.router)
    app.include_router(alerts.router)
    return app
