EXAMPLE1_dev_spec = {
        "outfields" : [
            "md5sum",
            "archive_filename",
            "exposure",
            "ifilter",
            "AIRMASS",
            "G-TRANSP",
            "hdu:ra_center",
            "hdu:ra_min",
            "hdu:ra_max",
            "hdu:dec_min",
            "hdu:dec_max",
            "hdu:FWHM",
            "hdu:AVSKY"
        ],
        "search" : [
            ["hdu:ra_center", -400, 400],
            ["caldat", "2018-09-01", "2020-12-31"] ,
            ["instrument", "decam"],
            ["proc_type", "raw"],
            ["prod_type", "image"],
            ["obs_type", "object"],
            ["proposal", "2019A-0305"],
            ["ifilter", "z DECam", "contains"]
        ],
        "COMMENT": "This spec contains examples of all features. Can only be used on rectype=Hdu"}
