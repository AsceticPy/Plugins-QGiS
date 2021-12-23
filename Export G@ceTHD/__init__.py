from PyQt5.QtWidgets import QAction, QMessageBox, QInputDialog, QLineEdit
import psycopg2
import os

cur_path = os.path.dirname(os.path.abspath(__file__))

def classFactory(iface):
    return MinimalPlugin(iface)


class MinimalPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('Export', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        qid = QInputDialog()
        mode = QLineEdit.Normal

        title = "Entrez la zone à exporter"
        label = "Zone: "
        #default = "<zn_code ou zs_code>"
        default = "ZN060100000000"

        #QMessageBox.information(None, 'Minimal plugin', 'Do something useful here')
        zone, ok = QInputDialog.getText(qid, title, label, mode, default)

        if ok and zone:
            def set_connexion() -> psycopg2.connect:
                return psycopg2.connect(database=db, user=user, password=pwd, host=host, port=port0)

            def close_connection():
                connexion.close()

            with open(cur_path + r"\conf\connection.txt", "r") as con_file:
                host = con_file.readline().strip().split(':')[1]
                user = con_file.readline().strip().split(':')[1]
                db = con_file.readline().strip().split(':')[1]
                pwd = con_file.readline().strip().split(':')[1]
                port0 = con_file.readline().strip().split(':')[1]

            

            def msgbox(msg: str, title: str):
                QMessageBox.information(None, title, msg)

            def get_query(query_file: str) -> list:
                cursor = connexion.cursor()
                with open(query_file, "r") as data_file:
                    query_list: str = []
                    while True:
                        line0 = data_file.readline().strip()
                        if not line0:
                            break
                        query_list.append(line0)
                cursor.close()
                return query_list

            def reset_export():
                cursor = connexion.cursor()
                query = get_query(cur_path + r"\conf\raz_export.txt") 
                for q in query:
                    if q:
                        cursor.execute(q)
                connexion.commit()
                cursor.close()

            def set_export(type_zone: str, zone: str) -> bool:
                cursor = connexion.cursor()
                if type_zone == 'ZN':
                    query = get_query(cur_path + r"\conf\export_nro.txt")
                else:
                    query = get_query(cur_path + r"\conf\export_sro.txt")

                # try:
                #     for q in query:
                #         if "%s" in q:
                #             #q.format(zone)
                #             cursor.execute(q, zone)
                #         else:
                #             cursor.execute(q)
                #         #print(cursor.statutmessage)
                #     connexion.commit()
                #     cursor.close()
                #     return True
                # except:
                #     cursor.close()
                #     return False

                for q in query:
                    print(q)
                    if "%s" in q:
                        #q.format(zone)
                        cursor.execute(q, (zone,))
                    else:
                        cursor.execute(q)
                connexion.commit()
                return True

            def zone_exist(type_zone: str, zone: str) -> bool:
                print(type_zone, zone)
                cursor = connexion.cursor()

                if type_zone == "ZN":
                    QS = "SELECT zn_code FROM t_znro WHERE zn_code = '" + zone + "';"
                elif type_zone == "ZS":
                    QS = "SELECT zs_code FROM t_zsro WHERE zs_code = '" + zone + "';"
                else:
                    msgbox("Type de zone inconnu", "Erreur")
                    return False

                #if cursor.closed:
                #    cursor = connexion.cursor()

                cursor.execute(QS)

                if cursor.description is None:
                    msgbox("Zone introuvable dans la base de données.", "Erreur")
                    cursor.close()
                    return False

                cursor.close()
                return True

            def main(zone: str):
                type_zone = ''
                type_zone = type_zone.join([zone[i] for i in range(2)])

                if zone_exist(type_zone, zone):
                    reset_export()
                    if set_export(type_zone, zone):
                        msgbox("Export terminé", "Succès")
                    else:
                        msgbox("Un soucis est survenue lors de l'export", "Erreur")

                close_connection()

            connexion = set_connexion()
            main(zone)