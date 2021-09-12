db = db.getSiblingDB('cz_realestate')

db.bezrealitky.update({},{$unset: {"coordinates": 1}}, false, true)