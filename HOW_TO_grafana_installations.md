Additional information about installation Grafana with image renderer plugin. 

## Thank you
Thank you for sharing and contribution:
- [Dorlas](https://github.com/Dorlas)

## command grafana-cli plugins install grafana-image-renderer
From [Dorlas](https://github.com/Dorlas) feedback:

When I installed the plugin grafana-image-renderer (with command grafana-cli plugins install grafana-image-renderer) the program don't work well.
I had to figure out why - the answer was in the grafana log (/var/log/grafana/grafana.log).
After several tries I found what libraries are missing:

libnss3.so


libatk-1.0.so.0


libatk-bridge-2.0.so.0

libcups.so.2

libxkbcommon.so.0

libXcomposite.so.1

libXdamage.so.1

libXfixes.so.3

libXrandr.so.2

libgbm.so.1

libpango-1.0.so.0

libasound.so.2

In your system the best way - see all missing libraries by command:
ldd /var/lib/grafana/plugins/grafana-image-renderer/chrome-linux/chrome

And next more and more apt/yum search && apt/yum install .

## k8s with helm
Using the following [helm chart](https://artifacthub.io/packages/helm/grafana/grafana) to install 
Grafana with image renderer plugin to k8s cluster.  

Add repo to helm:
```helm repo add grafana https://grafana.github.io/helm-charts```

Install Grafana with image renderer plugin: 
```helm install grafana-i-r grafana/grafana --set imageRenderer.enabled=true```

My recommendation is set the following parameters also:
- --set persistence.enabled=true
- --set persistence.size=1Gi
- --set service.clusterIP={Your static clustered IP for Grafana} 

Fow more information please refer the helm chart [documentation](https://artifacthub.io/packages/helm/grafana/grafana#configuration)


