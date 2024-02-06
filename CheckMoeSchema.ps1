# start-docker.ps1

# input interactively
Write-Host -NoNewline -ForegroundColor Yellow "Enter the REST endpoint: "
$rest_endpoint = Read-Host
Write-Host -NoNewline -ForegroundColor Yellow "Enter the Deployment Name: "
$deployment = Read-Host
Write-Host -NoNewline -ForegroundColor Yellow "Enter the API key: "
$api_key = Read-Host 
$example_path = "./testdata/example.json"

$dockerImageName = "python-env:latest"
# check whether docker image exists.
$existingImage = docker images -q $dockerImageName

if (-not ($existingImage)) {
  docker image build . -t python-env
  Write-Host "docker image build succeeded."
}

# execute download-swagger.py
docker run -v ${pwd}:/app -w /app python-env:latest bash -c "python download-swagger.py --rest_endpoint $rest_endpoint --deployment $deployment --api_key $api_key"

if (-not (Test-Path $example_path)) {
  echo "================"
  Write-Host -NoNewline -ForegroundColor Yellow "Enter the testdata(.csv) path ※eg.) ./testdata/hoge.csv: "
  $testdata = Read-Host
  echo "================"
  python get-example.py --testdata $testdata

}
# startup docker
docker ps -q | ForEach-Object { docker stop $_ >$null }
docker run -d -p 5050:5050 -v ${pwd}/swagger/:/usr/share/nginx/html/api -e API_URL=api/swagger_spec.json swaggerapi/swagger-ui

# wait until docker container start complete.
$containerRunning = $false
while (-not $containerRunning) {
    $containerRunning = docker ps -q | ForEach-Object { docker inspect --format '{{.State.Running}}' $_ } -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

# automatically access to localhost
Start-Process 'http://localhost:8080'
