Building this program as a full-scale web application, rather than a command-line program, requires consideration of concerns like performance at scale and availability. To tackle these concerns I would build the application in two parts: a back-end service and a web-based user interface. The back-end service would handle retrieving and filtering the data, and the web-based user interface would generate calls to the back-end service and display the results. The front-end would defer the expensive computation to the back-end, rather than the browser, to better present a responsive interface to the user. I would build the back-end service using a cloud computing platform (e.g. Amazon Web Services). A distributed cloud computing environment helps achieve performance at scale, as increased load can be offset by additional instances of the service.  

To ensure high availability I would design the back-end service to not be reliant on the up-time of the DataSF API endpoint. Specifically, I would have the back-end service periodically pull down and store the food truck data. When the back-end service then receives a request for data, the data can be served from the locally-stored copy. Thus the service is not interrupted if DataSF API endpoint were to become unresponsive or slow. High availability can be further helped by the cloud computing platform, as service failures can be automatically detected and a restart performed.