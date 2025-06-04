# Extract Variable

def renderBanner(self):
    is_mac = self.platform.toUpperCase().indexOf("MAC") > -1
    is_ie = self.browser.toUpperCase().indexOf("IE") > -1
    initialized = self.wasInitialized()
    should_resize = self.resize > 0
    if is_mac and is_ie and initialized and should_resize:
        # do something
