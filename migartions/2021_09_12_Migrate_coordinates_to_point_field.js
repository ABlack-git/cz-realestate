db = db.getSiblingDB('cz_realestate')

db.bezrealitky.find().forEach(
    function(x) {
        x.coords = {type: "Point", coordinates: [x.coordinates.lon, x.coordinates.lat]}
        db.bezrealitky.save(x)
    }
)