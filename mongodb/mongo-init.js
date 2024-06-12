db = new Mongo().getDB(process.env.MONGO_DB_NAME);

db.createUser({
    user: process.env.MONGO_USER_NAME,
    pwd: process.env.MONGO_USER_PWD,
    roles: [
        {
            role: 'readWrite',
            db: process.env.MONGO_DB_NAME
        }
    ]
});

db.createCollection(process.env.MONGO_TABLE_NAME, {capped: false});