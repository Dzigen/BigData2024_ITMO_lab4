db = new Mongo().getDB(process.env.MONGO_MODELDB_NAME);

db.createUser({
    user: process.env.MONGO_MODELDB_USER_USERNAME,
    pwd: process.env.MONGO_MODELDB_USER_PASSWORD,
    roles: [
        {
            role: 'readWrite',
            db: process.env.MONGO_MODELDB_NAME
        }
    ]
});

db.createCollection(process.env.MONGO_TABLE_NAME, {capped: false});