from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = conectar()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        conn = conectar()
        conn.execute("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                     (nombre, categoria, precio, stock))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('form.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar()

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        conn.execute("""
            UPDATE productos 
            SET nombre=?, categoria=?, precio=?, stock=?
            WHERE id=?
        """, (nombre, categoria, precio, stock, id))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    producto = conn.execute("SELECT * FROM productos WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('form.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)