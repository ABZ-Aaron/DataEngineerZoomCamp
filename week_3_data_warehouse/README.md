## Dare Warehouses & BigQuery

* OLAP

   `Online Transaction Processing` is used to control and run essential business operations in real time. The updates are short and fast, and initiated by users. These are typically normalized databases for efficiency, and are generally small if historical data is analyzed. 

   They typically require rgular backups to ensure business continuity, and meet legal and governance requirements. They increase productivity of end users and the data lists day-to-day business transactions.

* OLAP

    `Online Analytical Processing` is used to plan, solve problems, support decisions and discover hidden insights. Data is periodically refereshed with scheduled, long-running batch jobs. They are typically denormalizd for analysis. They are generally large due to aggregating large data.

    Lost data can typically be reloded from OLTP databases as needed. They typically increase productivity for managers, data analysts, data scientists etc. They show a multidimensional view of enterprise data. 

So what is a Data Warehouse?

These are **OLAP** solutions. They are used for reporting and data analysis. Generally they have many data sources. All of these report to a staging area, before being pushed to the Data Warehouse. Data here is typically then output to Data Marts (e.g. purchasing, sales, inventory) for different teams to pull from. Although Data Scientists and Analysts may pull directly from the warehouse itself. 

So what is BigQuery?

This is a Data Warehouse solution by Google. 

* It is serverless, in that there are no servers to manage or database software to install. 
* Scalability and high-availability prioritised
* Features included like Machine Learning, Business Intelligence, and Geospatial Analysis. 
* BigQuery maximises flexibility by seperating the compute engine that analyses your data from your storage. 

BigQuery has an on demand pricing model (1 TB of data processing for $5) or a flat based rate (100 slots equalts $2000 per month, which is about 400 TB data processed)
