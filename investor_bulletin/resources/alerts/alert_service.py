""" Rule Service"""

"""_summary_
this file to write any business logic for the Rules
"""
from collections import defaultdict
from sqlalchemy.orm import Session
from resources.market.market_schema import Market
from resources.alert_rules.alert_rule_schema import AlertRuleResponse
from resources.alerts.alert_schema import AlertCreate, AlertResponse
from resources.alerts import alert_dal as alert_repository
from resources.alert_rules import alert_rule_service as rule_service
from resources.market import market_service


def create_alert(alert: AlertCreate, session: Session) -> AlertResponse:
    db_alert = alert_repository.create_alert(alert, session)
    if not db_alert:
        return None

    return AlertResponse.model_validate(db_alert)


def get_alerts(offset: int, limit: int, session: Session) -> list[AlertResponse]:
    db_alerts = alert_repository.get_alerts(offset, limit, session)
    alerts = []

    for db_alert in db_alerts:
        alerts.append(AlertResponse.model_validate(db_alert))

    return alerts


# helper function to trigger creating alerts
def trigger_alert_creation(session: Session) -> list[AlertResponse]:
    # fetch stocks data
    tickers_data = market_service.get_market_data()

    # get all alert rules
    rules = rule_service.get_all_alert_rules(session)

    # check if any stock passes given alert rules
    alerts = check_alerts(tickers_data, rules)

    created_alerts = []
    # create alerts for passing stocks
    for alert in alerts:
        created_alerts.append(create_alert(alert, session))

    return created_alerts


# helper function to check price crossover for ticker accroding to alert rules
def check_alerts(
    tickers_data: list[Market], rules: list[AlertRuleResponse]
) -> list[AlertCreate]:

    alerts = []

    # convert alert rule list into a map/dict
    # {"AAPL": [150, 160], "MSFT": [300]}  # Both rules are stored
    rule_map = defaultdict(list)

    for rule in rules:
        rule_map[rule.symbol].append(rule.threshold_price)

    for ticker in tickers_data:
        symbol = ticker.symbol
        price = ticker.price

        if symbol in rule_map:
            for threshold_price in rule_map[symbol]:
                # check crossover
                if price >= threshold_price:
                    alerts.append(
                        AlertCreate(
                            symbol=symbol,
                            trigger_price=price,
                            threshold_price=threshold_price,
                        )
                    )

    return alerts
