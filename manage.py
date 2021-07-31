from instance.config import Person
import view
from app import app
from share import share
if __name__ == "__main__":
    app.run(
        host=Person.HOST,
        port=Person.PORT,
        debug=Person.DEBUG
    )
else:
    pass
