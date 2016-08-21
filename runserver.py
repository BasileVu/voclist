from voclist import app, db, setup_app

__author__ = "Basile Vu <basile.vu@gmail.com>"

if __name__ == "__main__":
    setup_app("config/voclist.cfg")
    db.create_all()
    app.run(debug=True)
