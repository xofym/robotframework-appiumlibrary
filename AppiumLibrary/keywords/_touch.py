# -*- coding: utf-8 -*-

from appium.webdriver.common.touch_action import TouchAction

from AppiumLibrary.locators import ElementFinder
from .keywordgroup import KeywordGroup


class _TouchKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def pinch(self, locator, percent="200%", steps=1):
        """
        Pinch in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.pinch(element=element, percent=percent, steps=steps)

    def swipe(self, start_x, start_y, offset_x, offset_y, duration=1000):
        """
        Swipe from one point to another point, for an optional duration.

        Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - offset_x - x-coordinate distance from start_x at which to stop
         - offset_y - y-coordinate distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.

        Usage:
        | Swipe | 500 | 100 | 100 | 0 | 1000 |

        _*NOTE: *_
        Android 'Swipe' is not working properly, use ``offset_x`` and ``offset_y`` as if these are destination points.
        """
        driver = self._current_application()
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)

    def swipe_by_percent(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        Swipe from one percent of the screen to another percent, for an optional duration.
        Normal swipe fails to scale for different screen resolutions, this can be avoided using percent.

        Args:
         - start_x - x-percent at which to start
         - start_y - y-percent at which to start
         - end_x - x-percent distance from start_x at which to stop
         - end_y - y-percent distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.

        Usage:
        | Swipe By Percent | 90 | 50 | 10 | 50 | # Swipes screen from right to left. |

        _*NOTE: *_
        This also considers swipe acts different between iOS and Android.

        New in AppiumLibrary 1.4.5
        """
        width = self.get_window_width()
        height = self.get_window_height()
        x_start = float(start_x) / 100 * width
        x_end = float(end_x) / 100 * width
        y_start = float(start_y) / 100 * height
        y_end = float(end_y) / 100 * height
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        platform = self._get_platform()
        if platform == 'android':
            self.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.swipe(x_start, y_start, x_offset, y_offset, duration)

    def scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)

    def scroll_down(self, locator):
        """Scrolls down to element"""
        self.scroll_dir(locator=locator, direction='down')

    def scroll_up(self, locator):
        """Scrolls up to element"""
        self.scroll_dir(locator=locator, direction='up')

    def scroll_down_in(self, locator, scroll_locator=None, max_iteration=1):
        """Scrolls down in scrollview to element"""
        platform = self._get_platform()
        if platform == 'android':
            driver = self._current_application()
            if locator.find("=") >= 0:
                el_desc = locator.split("=")[1]
            else:
                el_desc = locator 
            if scroll_locator.find("=") >= 0:
                scroll_desc = scroll_locator.split("=")[1]
            else:
                scroll_desc = locator 
            driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().descriptionContains("'+scroll_desc+'")).scrollIntoView(new UiSelector().descriptionContains("'+el_desc+'"))')
        elif platform == 'ios':
            self.search_and_display_ios_element(locator=locator,max_iteration=max_iteration)

    def long_press(self, locator, duration=1000):
        """ Long press the element with optional duration """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.press(element).wait(duration).release().perform()

    def tap(self, locator, x_offset=None, y_offset=None, count=1):
        """ Tap element identified by ``locator``.

        Args:
        - ``x_offset`` - (optional) x coordinate to tap, relative to the top left corner of the element.
        - ``y_offset`` - (optional) y coordinate. If y is used, x must also be set, and vice versa
        - ``count`` - can be used for multiple times of tap on that element
        """
        driver = self._current_application()
        el = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.tap(el,x_offset,y_offset, count).perform()

    def click_a_point(self, x=0, y=0, duration=100):
        """ Click on a point"""
        self._info("Clicking on a point (%s,%s)." % (x,y))
        driver = self._current_application()
        action = TouchAction(driver)
        try:
            action.press(x=float(x), y=float(y)).wait(float(duration)).release().perform()
        except:
            assert False, "Can't click on a point at (%s,%s)" % (x,y)

    def click_element_at_coordinates(self, coordinate_X, coordinate_Y):
        """ click element at a certain coordinate """
        self._info("Pressing at (%s, %s)." % (coordinate_X, coordinate_Y))
        driver = self._current_application()
        action = TouchAction(driver)
        action.press(x=coordinate_X, y=coordinate_Y).release().perform()

    # Private

    def scroll_dir(self, locator, direction):
        """Scrolls to element in given direction"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": direction, 'element': element.id})

    def search_and_display_ios_element(self, locator, max_iteration=1):
        #ios strategy:
        #1) check if element is in view hierarchy
        #   => if not error
        #2) check if visible
        #   => if so the stop searching
        #3) scroll a screen height
        #4) check if visible
        #   => if so the stop searching
        #5) scroll a screen height
        #6) check if visible
        #   => if so the stop searching
        #7) scroll a screen height
        element = self._element_find(locator, True, False)
        if element is not None:
            element_visible = element.is_displayed()
            #to be used later to process the ammount of scroll needed
            element_size = element.size
            element_location = element.location
            height = self.get_window_height()
            i = 0
            while i < max_iteration:
                i += 1
                self.swipe(start_x=0,start_y=height-200,offset_x=0,offset_y=-height,duration=3000)
                element_visible = element.is_displayed()
                if element_visible:
                    return
            raise AssertionError("Element '%s' could not be displayed without too much scrolling" % locator)
        else:
            raise AssertionError("Element '%s' could not be found" % locator)
            return None
            # screen_h = self.get_window_height()
            # screen_w = self.get_window_width()
            # position = self.get_element_location(locator=locator)
            # size = self.get_element_size(locator=locator)
            # el_h = size["height"]
            # offset = position["y"] + el_h - screen_h
            # offset = 10
            #self.scroll(start_locator="mountingAdvice_outdoorSiren_fixing_drill_step1_illustration",end_locator=locator)
            #self.swipe(start_x=0,start_y=screen_h-200,offset_x=0,offset_y=screen_h-220,duration=3000)
