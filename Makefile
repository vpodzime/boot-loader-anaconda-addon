updates-img:
	-@mkdir -p updates/usr/share/anaconda/addons
	@cp -r org_fedora_boot_loader updates/usr/share/anaconda/addons
	@cd updates; find . | cpio -c -o | gzip -9 > ../updates.img; cd ..
	-@rm -rf updates

