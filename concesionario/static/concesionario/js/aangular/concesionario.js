(function () {

	'use strict';

	angular
		.module('concesionario', [
			'concesionario.config',
			'concesionario.routes',
			'concesionario.controllers'
		]);

	angular
		.module('concesionario.config', []);

	angular
		.module('concesionario.routes', ['ngRoute']);

	angular
		.module('concesionario.controllers', []);

	angular
		.module('concesionario')
		.run(run);

	run.$inject = ['$http'];


	function run($http) {
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';
	}
})();