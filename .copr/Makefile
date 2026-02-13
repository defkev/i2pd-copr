pkgs:
	dnf -y install fedpkg git rpmautospec rpmdevtools

sources: pkgs
	spectool --gf i2pd.spec

srpm: sources
	git config --global --add safe.directory .
	fedpkg --release f40 srpm
	cp *.src.rpm $(outdir)
