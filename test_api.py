from model import ExRate

def update_xrates(from_currency, to_currency):
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, ExRate.to_currency == to_currency).first()
    print(f"xrate before: {xrate}")
    xrate.rate += 0.01
    xrate.save()
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, ExRate.to_currency == to_currency).first()
    print(f"xrate after: {xrate}")

