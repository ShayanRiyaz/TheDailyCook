if [ ! -d 'venv' ];
then
	echo -------------------------
	python -m venv venv
	echo -------------------------
	echo virtual environment ready
fi
source venv/bin/activate


if [ -f "requirements.txt" ];
then 
	echo --------------------------
	echo Installing requirements
	pip install -r requirements.txt
	echo --------------------------
fi