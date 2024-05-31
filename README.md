# userbars-be
 
The *userbars-be.py* file downloads every userbar from the website *www.userbars.be* and generates a JSON file with the metadata associated to it.

More specifically, it saves the following information:
- **Userbar unique number**
- **Download link**
- **Title**
- **Uploader name**
- **Upload date**
- **Category**

The downloaded userbars get saved in a *userbars-be/* folder.

# userbars-name

The *userbars-name.py* saves information about the userbars on the website *www.userbars.name* and generates a JSON file with the metadata associated to them, saving it in a *userbars-name/data* folder, as well as a text file with the URLs of the userbars.

Most of the userbars are hosted on Imgur and downloading them with Python is not easy. Therefore, it is recommended to download them using [gallery-dl](https://github.com/mikf/gallery-dl), feeding it with the output text file like this:

````
gallery-dl -i userbars-name.txt

````

## Dependencies

All the necessary libraries are listed in the *requirements.txt* file.

You can install them by running:

```
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/userbars-downloader/blob/main/LICENSE) file for details.


# Update
As of [June 2023](https://cohost.org/andrewelmore/post/1668013-r-i-p-userbars-be), the website is down.
