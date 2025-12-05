#  Solución Automatizada para Respaldo y Monitoreo de Bases de Datos Financieras

Este proyecto implementa una solución modular para respaldar y monitorear bases de datos financieras utilizando tecnologías modernas de infraestructura: **PostgreSQL, Docker, Apache Airflow y Grafana**. La base de datos utilizada es *Financial*, proveniente del [CTU Relational Repository](https://relational.fel.cvut.cz/dataset/Financial), que simula operaciones bancarias reales.

## Características principales
- Respaldos confiables de la base *Financial*  
- Automatización con Airflow de respaldos completos, diferenciales e incrementales  
- Monitoreo en tiempo real con Grafana  
- Seguridad reforzada mediante usuarios y credenciales protegidas en `.env`  
- Consultas optimizadas para análisis rápido de transacciones  

## Tecnologías utilizadas
- PostgreSQL: motor relacional para almacenar y gestionar datos financieros  
- Docker & Docker Compose: despliegue portable y reproducible de servicios  
- Apache Airflow: orquestación de flujos de respaldo y consultas periódicas  
- Grafana: visualización de métricas y estado de respaldos  


## Modalidades de respaldo
- Completo: copia total de la base (`pg_dump`)  
- Diferencial: cambios desde el último respaldo completo  
- Incremental: cambios desde el último respaldo cualquiera (`pg_basebackup`)  

Los respaldos se ejecutan automáticamente mediante DAGs en Airflow y se almacenan en volúmenes persistentes de Docker.

## Monitoreo y consultas
- Grafana: paneles para métricas en tiempo real  
- Airflow logs: auditoría de ejecución de DAGs  
- Consulta periódica (`consulta_basica.py`): muestra los últimos 15 registros de la tabla `trans` para validar disponibilidad y eficiencia  

## Instalación y uso
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/nana-mor/ProyectoFinalABD.git
   cd ProyectoFinalABD
   ```
2. Configurar credenciales en el archivo `.env`

3.  Levantar servicios con Docker Compose:
   ```bash
   docker-compose up -d
   ```
4. Acceder a:
- Airflow Webserver: `http://localhost:8080`
- Grafana: `http://localhost:3000`
##  Conclusiones

Este sistema ofrece una solución práctica y extensible para evitar la pérdida de información financiera:

- Confiabilidad: respaldos automáticos y recuperación garantizada
- Seguridad: control de accesos y auditoría de logs
- Escalabilidad: infraestructura modular adaptable
- Eficiencia: consultas optimizadas para análisis rápido

## Referencias

- Docker Documentation
- Apache Airflow Documentation
- PostgreSQL Documentation
- Grafana Documentation
