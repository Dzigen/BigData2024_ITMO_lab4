db = new Mongo().getDB('modelapi_log');

db.createUser({
    user: 'dzigen',
    pwd: 'password',
    roles: [
        {
            role: 'readWrite',
            db: 'modelapi_log'
        }
    ]
});

db.createCollection('saved_requests', {capped: false});