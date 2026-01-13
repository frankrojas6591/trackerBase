from tracker import create_app

app = create_app()

if __name__ == '__main__':
    print("run.py")
    app.run(debug=True)
