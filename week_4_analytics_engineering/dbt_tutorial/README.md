# DBT Fundamentals

## Who is an Analytics Engineer?

Traditional data teams have data engineers (build the infrastructure and ETL) and data analysts (query the data, create dashboards, Excel, and reporting). 

There's a gap between the two of them. The analysts know what needs to be built. The data engineer knows how to build it. 

What is ETL? Extract, Transform and Load data.

What is ELT? Extract, Load, and Transform data.

Enter cloud-based data warehouses. These combine a database and a supercomputer for transforming the data. ELT shifts focus to getting data in warehouse and transforming the data from there (ELT). 

The compute and storage for DW is scalable. There's also a reduction of transfer time.

With an Analytics Engineer, they focus on taking raw data and transforming it for analysts. There is charge of the T in ELT. 

The DE can then focus on extracting and loading data into data warehouse. The analysts can work more closely with the AE to deliver dashboards and reporting to stakeholders.

So a modern data stack looks like data engineers, data analysts, and analytics engineers.

### DBT

So how does DBT fit into this modern data stack?

```
Data Sources --> Loaders --> Data Platforms --> BI Tools or ML Models
```

In the above, DBT works with our Data Platforms.

With DBT, we use this to develop our transformation pipeline using SELECT statements. We can use DBT to test and document our models. 

### Exemplar Project


## Set up DBT Cloud

## Models

## Sources

## Tests

## Documentation

## Deployment