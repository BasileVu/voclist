from voclist import app, db

__author__ = "Basile Vu <basile.vu@gmail.com>"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
