# {py:mod}`indradaily.emails`

```{py:module} indradaily.emails
```

```{autodoc2-docstring} indradaily.emails
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`send_email <indradaily.emails.send_email>`
  - ```{autodoc2-docstring} indradaily.emails.send_email
    :summary:
    ```
* - {py:obj}`data_upload_email <indradaily.emails.data_upload_email>`
  - ```{autodoc2-docstring} indradaily.emails.data_upload_email
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <indradaily.emails.logger>`
  - ```{autodoc2-docstring} indradaily.emails.logger
    :summary:
    ```
* - {py:obj}`__all__ <indradaily.emails.__all__>`
  - ```{autodoc2-docstring} indradaily.emails.__all__
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: indradaily.emails.logger
:value: >
   'getLogger(...)'

```{autodoc2-docstring} indradaily.emails.logger
```

````

````{py:function} send_email(recipients: dict, subject: str, body: str, config: dict, attachment: bool = False, attachment_path: typing.Optional[str] = None, from_name: typing.Optional[str] = 'Automatic Notifications | DSIH Admin')
:canonical: indradaily.emails.send_email

```{autodoc2-docstring} indradaily.emails.send_email
```
````

````{py:function} data_upload_email(upload_success: bool, recipients: dict, dataset_name: str, dataset_source: str, no_files: int, latest_timestamp: datetime.datetime, attachment: bool = False)
:canonical: indradaily.emails.data_upload_email

```{autodoc2-docstring} indradaily.emails.data_upload_email
```
````

````{py:data} __all__
:canonical: indradaily.emails.__all__
:value: >
   ['data_upload_email', 'send_email']

```{autodoc2-docstring} indradaily.emails.__all__
```

````
