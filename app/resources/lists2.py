db.lists.insertMany([
    {
        {
        'id':0,
        'todos':[{
                    'id':0,
                    'task':{
                        'name':'Eat',
                        'created_on':'29/02/2020'
                    }
                },
                {
                    'id':1,
                    'task':{
                        'name':'Sleep',
                        'created_on':'01/03/2020'
                    }
                },
                {
                    'id':2,
                    'task':{
                        'name':'Code',
                        'created_on':'02/03/2020'
                    }
                },
                {
                    'id':3,
                    'task':{
                        'name':'Compile (but compiling is doubting)',
                        'created_on':'02/03/2020'
                    }
                },
                {
                    'id':4,
                    'task':{
                        'name':'Repeat',
                        'created_on':'03/03/2020'
                    }
                }]
        },
        {
        'id':1,
        'todos':[{
                    'id':0,
                    'task':{
                        'name':'Born',
                        'created_on':'28/12/1998'
                    }
                },
                {
                    'id':1,
                    'task':{
                        'name':'Growing',
                        'created_on':'01/03/2000'
                    }
                },
                {
                    'id':2,
                    'task':{
                        'name':'Enjoy',
                        'created_on':'02/03/2010'
                    }
                }]
        }
    }
])