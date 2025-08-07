#!/usr/bin/env python3
# -------------  MIKROTIK TOOL GUI  -------------
#  * GUI en ttkbootstrap (tema darkly)
#  * Sin archivos .sh temporales: todo se hace vía SSH directo
#  * SCADA, DHCP, Rutas y monitor de ping conservados
# ------------------------------------------------
import subprocess, os, time, threading, serial, ttkbootstrap as tb
from ttkbootstrap import ttk
from tkinter import PhotoImage, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import font

# ---------- Parámetros de conexión ----------
SSH_USER = "admin"
SSH_PASS = "admin"
SSH_HOST = "10.0.0.20"
SSH_BASE = [
    "sshpass", "-p", SSH_PASS, "ssh",
    "-o", "StrictHostKeyChecking=no",
    f"{SSH_USER}@{SSH_HOST}"
]

# ---------- Helper SSH ----------
def run_ssh(cmd: str) -> str:
    res = subprocess.run(SSH_BASE + [cmd],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip() or "Error SSH")
    return res.stdout.strip()

# ---------- Ventana principal ----------
v0 = tb.Window(themename="darkly")
v0.title("ROUTER MIKROTIK")
v0.geometry("800x550+60+60")

f_big  = font.Font(family="Arial", size=18)
f_norm = font.Font(family="Arial", size=12)

tb.Label(v0, text="ROUTER MIKROTIK", font=f_big).place(x=170, y=5)

# ---------- Variables de entrada ----------
var_name  = tb.StringVar()
var_ip    = tb.StringVar()
var_iface = tb.StringVar()
var_comm  = tb.StringVar()

labels = [("Router name :", var_name, 100, 30),
          ("Ip address  :", var_ip,   150, 20),
          ("Interface   :", var_iface,190, 15),
          ("Comment     :", var_comm, 230, 20)]
for txt, var, y, wid in labels:
    tb.Label(v0, text=txt, font=f_norm).place(x=50, y=y)
    tb.Entry(v0, textvariable=var, width=wid).place(x=170, y=y)

# ---------- Área de salida ----------
txt_out = ScrolledText(v0, width=80, height=10)
txt_out.place(x=10, y=270)

def show_output(data: str):
    txt_out.delete("1.0", tb.END)
    txt_out.insert(tb.END, data)

# ---------- Acciones básicas ----------
def consulta_name():
    try:
        show_output(run_ssh("system identity print"))
    except Exception as e:
        messagebox.showerror("SSH", str(e))

def consulta_ip():
    try:
        show_output(run_ssh("ip address print"))
    except Exception as e:
        messagebox.showerror("SSH", str(e))

def save_name():
    new = var_name.get().strip()
    if not new:
        messagebox.showwarning("Dato vacío", "Ingresa un nombre.")
        return
    try:
        run_ssh(f"system identity set name={new}")
        messagebox.showinfo("OK", "Nombre cambiado.")
    except Exception as e:
        messagebox.showerror("SSH", str(e))

def save_addr():
    ipaddr = var_ip.get().strip()
    iface  = var_iface.get().strip()
    commt  = var_comm.get().strip()
    if not (ipaddr and iface):
        messagebox.showwarning("Dato vacío", "IP y/o Interface vacío.")
        return
    try:
        run_ssh(f"ip address add address={ipaddr} interface={iface} comment='{commt}'")
        messagebox.showinfo("OK", "Dirección añadida.")
    except Exception as e:
        messagebox.showerror("SSH", str(e))

def delete_addr():
    idx = combo_del.get().strip()
    if not idx.isdigit():
        messagebox.showwarning("Índice", "Selecciona un índice válido (1-5).")
        return
    try:
        run_ssh(f"ip address remove {idx}")
        messagebox.showinfo("OK", "Dirección eliminada.")
    except Exception as e:
        messagebox.showerror("SSH", str(e))

# ---------- Botones básicos ----------
tb.Button(v0, text="SAVE",  bootstyle="primary",
          command=save_name).place(x=430, y=100)
tb.Button(v0, text="SAVE",  bootstyle="primary",
          command=save_addr).place(x=430, y=200)
tb.Button(v0, text="QUERY", bootstyle="info",
          command=consulta_name).place(x=520, y=100)
tb.Button(v0, text="QUERY", bootstyle="info",
          command=consulta_ip).place(x=520, y=200)

# Combobox eliminar IP
combo_del = tb.StringVar()
ttk.Combobox(v0, textvariable=combo_del,
             values=[str(i) for i in range(1,6)]).place(x=400, y=150)
tb.Button(v0, text="X", bootstyle="danger",
          command=delete_addr).place(x=595, y=150)

# ---------- DHCP SERVER ----------
def ventana_dhcp():
    win = tb.Toplevel(v0)
    win.title("DHCP SERVER")
    win.geometry("500x400+100+100")
    campos = ("Pool", "Ranges", "DHCP name", "Iface",
              "Network", "Gateway", "DNS")
    vars_d = {c: tb.StringVar() for c in campos}
    for i,c in enumerate(campos):
        tb.Label(win, text=f"{c}:", font=f_norm).place(x=10, y=50+30*i)
        tb.Entry(win, textvariable=vars_d[c],
                 width=30 if c=="Ranges" else 20).place(x=120, y=50+30*i)

    def save_dhcp():
        v=vars_d
        try:
            run_ssh(f"ip pool add name={v['Pool'].get()} ranges={v['Ranges'].get()}")
            run_ssh(f"ip dhcp-server add name={v['DHCP name'].get()} interface={v['Iface'].get()} "
                    f"address-pool={v['Pool'].get()} disabled=no")
            run_ssh(f"ip dhcp-server network add address={v['Network'].get()} "
                    f"gateway={v['Gateway'].get()} dns-server={v['DNS'].get()}")
            messagebox.showinfo("OK", "DHCP creado.")
        except Exception as e:
            messagebox.showerror("SSH", str(e))

    tb.Button(win, text="SAVE", bootstyle="success",
              command=save_dhcp).place(x=380, y=50)

# ---------- RUTAS ----------
def ventana_rutas():
    win = tb.Toplevel(v0)
    win.title("RUTAS")
    win.geometry("400x200+100+100")
    dst = tb.StringVar(); gw = tb.StringVar()
    tb.Label(win, text="Dst-Addr:", font=f_norm).place(x=10, y=50)
    tb.Entry(win, textvariable=dst).place(x=120, y=50)
    tb.Label(win, text="Gateway:", font=f_norm).place(x=10, y=90)
    tb.Entry(win, textvariable=gw).place(x=120, y=90)

    def save_ruta():
        try:
            run_ssh(f"ip route add dst-address={dst.get()} gateway={gw.get()}")
            messagebox.showinfo("OK", "Ruta añadida.")
        except Exception as e:
            messagebox.showerror("SSH", str(e))

    tb.Button(win, text="SAVE", bootstyle="danger",
              command=save_ruta).place(x=200, y=130)

# ---------- SCADA ----------
def ventana_scada():
    win = tb.Toplevel(v0)
    win.title("SCADA")
    win.geometry("400x300+100+200")
    img_on  = PhotoImage(file="ethernetON.gif")
    img_off = PhotoImage(file="ethernetOFF.gif")
    lbl_img = tb.Label(win, image=img_off)
    lbl_img.place(x=20, y=100)

    lbl = tb.Label(win, text="OFF", font=f_norm, foreground="red")
    lbl.place(x=150, y=120)

    actualizar_estado_ping.lbl = lbl
    actualizar_estado_ping.lbl_img = lbl_img
    actualizar_estado_ping.img_on = img_on
    actualizar_estado_ping.img_off = img_off

    estado = tb.StringVar(value="0")
    actualizar_estado_ping.estado = estado

    def toggle():
        v = estado.get()
        if arduino and arduino.is_open:
            arduino.write(b"G" if v == "1" else b"R")
            arduino.flush()
        lbl.config(text="ON" if v == "1" else "OFF",
                   foreground="green" if v == "1" else "red")
        lbl_img.config(image=img_on if v == "1" else img_off)

    tb.Checkbutton(win, text="Monitor", variable=estado,
                   bootstyle="warning", command=toggle).place(x=20, y=50)

    # Esta línea es la clave:
    actualizar_estado_ping(hay_ping(SSH_HOST))

# ---------- Conexión Arduino ----------
try:
    arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
    time.sleep(2)
except Exception as e:
    arduino = None
    print("Serial:", e)

# ---------- Monitor de ping ----------
def hay_ping(ip):
    return subprocess.run(["ping","-c","1","-W","1",ip],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode==0

def actualizar_estado_ping(ok):
    if not hasattr(actualizar_estado_ping, "lbl") or not hasattr(actualizar_estado_ping, "estado"):
        return  # la GUI aún no fue inicializada

    lbl = actualizar_estado_ping.lbl
    estado = actualizar_estado_ping.estado
    estado.set("1" if ok else "0")
    lbl.config(text="ON" if ok else "OFF",
               foreground="green" if ok else "red")
    # Cambiar imagen
    if hasattr(actualizar_estado_ping, "lbl_img"):
        actualizar_estado_ping.lbl_img.config(
            image=actualizar_estado_ping.img_on if ok else actualizar_estado_ping.img_off
        )

def hilo_ping():
    prev=None
    while True:
        ok = hay_ping(SSH_HOST)
        cmd = b"G" if ok else b"R"
        if arduino and arduino.is_open and cmd != prev:
            arduino.write(cmd); arduino.flush()
            prev = cmd

        # Actualizar imagen y checkbutton en la interfaz
        v0.after(0, actualizar_estado_ping, ok)
        time.sleep(5)
threading.Thread(target=hilo_ping, daemon=True).start()

# ---------- Botones extra ----------
# Botones DHCP, RUTAS y SCADA (referenciados)
btn_dhcp  = tb.Button(v0, text="DHCP-SERVER", bootstyle="success", command=ventana_dhcp)
btn_rutas = tb.Button(v0, text="RUTAS",        bootstyle="danger",  command=ventana_rutas)
btn_scada = tb.Button(v0, text="SCADA",        bootstyle="warning", command=ventana_scada)

btn_dhcp.place(x=10, y=470)
btn_rutas.place(x=230, y=470)
btn_scada.place(x=140, y=470)

btn_rutas.place_forget()

v0.mainloop()
