from website import app
from database import persistent_DB_engine, volatile_RAM_engine, end_engines


# variables to decide the URL of the website
host = '127.0.0.1'
port_num = 5000
url = f"http://{host}:{port_num}"

# this function runs the flask server (hosting the website)
# to close the server, use ctrl + c to create a keyboard interrupt, 
# this will safely destroy all engine connections to the database
def run_app():
    print(url)
    try:
        app.run(
            host=host,
            port=port_num,
            debug=True
        )
    except KeyboardInterrupt:
        end_engines([persistent_DB_engine, volatile_RAM_engine])



# use python -m flask run to stop it raising warnings about how it should be deployed
if __name__ == "__main__":
    run_app()