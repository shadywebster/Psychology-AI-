import React, { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { View, Text, StyleSheet } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import * as Notifications from 'expo-notifications';

import HomeScreen      from './src/screens/HomeScreen';
import ChatScreen      from './src/screens/ChatScreen';
import JournalScreen   from './src/screens/JournalScreen';
import ExercisesScreen from './src/screens/ExercisesScreen';
import ProfileScreen   from './src/screens/ProfileScreen';
import { COLORS }      from './src/theme';

SplashScreen.preventAutoHideAsync();

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

const Tab = createBottomTabNavigator();

function TabIcon({ name, focused }: { name: string; focused: boolean }) {
  const icons: Record<string, string> = {
    Home: '⌂', Chat: '💬', Journal: '📓', Exercises: '🧘', Profile: '◉'
  };
  return (
    <Text style={{ fontSize: 20, opacity: focused ? 1 : 0.4 }}>
      {icons[name]}
    </Text>
  );
}

export default function App() {
  useEffect(() => {
    SplashScreen.hideAsync();
  }, []);

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <NavigationContainer>
          <StatusBar style="light" backgroundColor={COLORS.bg} />
          <Tab.Navigator
            screenOptions={({ route }) => ({
              headerShown: false,
              tabBarIcon: ({ focused }) => (
                <TabIcon name={route.name} focused={focused} />
              ),
              tabBarLabel: ({ focused, children }) => (
                <Text style={{
                  fontSize: 10,
                  fontWeight: '500',
                  color: focused ? COLORS.teal : COLORS.text3,
                  marginBottom: 4,
                }}>
                  {children}
                </Text>
              ),
              tabBarStyle: {
                backgroundColor: COLORS.bg2,
                borderTopColor: 'rgba(255,255,255,0.06)',
                borderTopWidth: 0.5,
                height: 72,
                paddingTop: 6,
              },
              tabBarActiveTintColor: COLORS.teal,
              tabBarInactiveTintColor: COLORS.text3,
            })}
          >
            <Tab.Screen name="Home"      component={HomeScreen}      />
            <Tab.Screen name="Chat"      component={ChatScreen}      />
            <Tab.Screen name="Journal"   component={JournalScreen}   />
            <Tab.Screen name="Exercises" component={ExercisesScreen} />
            <Tab.Screen name="Profile"   component={ProfileScreen}   />
          </Tab.Navigator>
        </NavigationContainer>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
