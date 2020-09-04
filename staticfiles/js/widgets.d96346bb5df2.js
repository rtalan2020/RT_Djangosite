fetch("{% static 'js/widgets.js' }", {
	"method": "GET",
})
.then(response => {
	console.log(response.text);
})
.catch(err => {
	console.log(err);
});