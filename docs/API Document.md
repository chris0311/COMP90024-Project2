# API Documentation

## Reformat Date in BOM Dataset

### `/redate`
- **Method**: POST
- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "date": "Str"
  }

- **Purpose**: Reformat date in the BOM dataset to standard Elastic Search date format

## Reformat Date in Mastodon Dataset

### `/mredate`

- **Method**: POST

- Headers:

  - `Content-Type: application/json`

- Request Body:

  ```json
  {
    "date": "Str"
  }
  ```

- **Purpose**: Reformat date in the BOM dataset to standard Elastic Search date format

## Remove HTTP Delimiters

### `/mpreprocess`

- **Method**: POST/GET

- Headers:

  - `Content-Type: application/json`

- Request Body:

  ```json
  {
    "text": "Str"
  }
  ```

- **Purpose**: Remove HTTP delimiters from text

## Get Sentiment Score

### `/sentiment`

- **Method**: POST/GET

- Headers:

  - `Content-Type: application/json`

- Request Body:

  ``` json
  code{
    "text": "Str"
  }
  ```

- **Purpose**: Get a sentiment score of a text

## Add New Data

### `/adddata`

- **Method**: POST

- Headers:

  - `Content-Type: application/json`

- Request Body:

  ``` json
  {
    "data": "JSON file"
  }
  ```

- **Purpose**: Add new data to the Elastic Search Cluster

## Query Observations Index

### `/bomquery/{start_date}/{end_date}?size={size}`

- **Method**: GET
- **Headers**: None
- **Request Body**: None
- **Purpose**: Query the Observations index

## Query Mastodon Index

### `/mquery/{start_date}/{end_date}?size={size}`

- **Method**: GET
- **Headers**: None
- **Request Body**: None
- **Purpose**: Query the Mastodon index

## Create Concatenated Dataset

### `/concat/{start_date}/{end_date}?size={size}&bsize={bsize}&msize={msize}`

- **Method**: GET
- **Headers**: None
- **Request Body**: None
- **Purpose**: Create a concatenated dataset from Observations and Mastodon index

## Return Median Age

### `/sa2/{sa2_code}/age`

- **Method**: GET
- **Headers**: None
- **Request Body**: None
- **Purpose**: Return the median age given a sa2_code

## Bulk Query Median Age

### `/sa2/age`

- **Method**: GET

- Headers:

  - `Content-Type: application/json`

- Request Body:

  ``` json
  {
    "sa2_codes": []
  }
  ```

- **Purpose**: Bulk API, query median age for a list of sa2_codes