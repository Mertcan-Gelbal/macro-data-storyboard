import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, ActivityIndicator, SafeAreaView, Dimensions } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import axios from 'axios';
import { VictoryLine, VictoryChart, VictoryAxis, VictoryTheme, VictoryTooltip, VictoryVoronoiContainer } from 'victory-native';
import { TrendingUp, Globe, Settings, ArrowUpRight, ArrowDownRight } from 'lucide-react-native';

const API_BASE = "/api";

export default function App() {
  const [indicators, setIndicators] = useState([]);
  const [selectedSymbol, setSelectedSymbol] = useState("sp500");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch Indicators Catalog
  useEffect(() => {
    axios.get(`${API_BASE}/indicators`)
      .then(res => setIndicators(res.data))
      .catch(err => console.log("Catalog Error:", err));
  }, []);

  // Fetch Detail Data for Selected Asset
  useEffect(() => {
    setLoading(true);
    axios.get(`${API_BASE}/data/${selectedSymbol}?horizon=1Y`)
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError("Network Error: Could not reach API server.");
        setLoading(false);
      });
  }, [selectedSymbol]);

  const renderCard = (asset) => (
    <TouchableOpacity 
      key={asset.id} 
      style={[styles.card, selectedSymbol === asset.id && styles.activeCard]}
      onPress={() => setSelectedSymbol(asset.id)}
    >
      <View style={styles.cardInfo}>
        <Text style={styles.cardCategory}>{asset.category.toUpperCase()}</Text>
        <Text style={styles.cardName}>{asset.name}</Text>
      </View>
      <ArrowUpRight size={18} color={selectedSymbol === asset.id ? "#58A6FF" : "#30363D"} />
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />
      
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerLabel}>INSTITUTIONAL CORE</Text>
          <Text style={styles.headerTitle}>Global Terminal</Text>
        </View>
        <TouchableOpacity style={styles.settingsBtn}>
          <Settings color="#8B949E" size={24} />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {/* Main Chart Section */}
        <View style={styles.chartContainer}>
          {loading ? (
            <ActivityIndicator size="large" color="#58A6FF" style={{ height: 300 }} />
          ) : data ? (
            <View>
              <View style={styles.chartHeader}>
                <Text style={styles.chartTitle}>{data.name}</Text>
                <View style={styles.priceRow}>
                  <Text style={styles.priceText}>{data.stats.latest.toFixed(2)}</Text>
                  <View style={[styles.changeBadge, { backgroundColor: data.stats.change_pct >= 0 ? '#1F332E' : '#331F1F' }]}>
                    <Text style={[styles.changeText, { color: data.stats.change_pct >= 0 ? '#3FB950' : '#F85149' }]}>
                      {data.stats.change_pct >= 0 ? "+" : ""}{data.stats.change_pct.toFixed(2)}%
                    </Text>
                  </View>
                </View>
              </View>
              
              <VictoryChart
                height={260}
                width={Dimensions.get('window').width - 40}
                theme={VictoryTheme.material}
                containerComponent={<VictoryVoronoiContainer />}
              >
                <VictoryAxis style={{ axis: { stroke: "none" }, tickLabels: { fill: "none" } }} />
                <VictoryLine
                  data={data.series}
                  style={{
                    data: { stroke: "#58A6FF", strokeWidth: 2 }
                  }}
                  animate={{ duration: 500 }}
                />
              </VictoryChart>
            </View>
          ) : (
            <Text style={styles.errorText}>{error || "Initialize selection..."}</Text>
          )}
        </View>

        {/* Assets List */}
        <View style={styles.listSection}>
          <Text style={styles.sectionTitle}>Asset Registry</Text>
          {indicators.map(renderCard)}
        </View>
      </ScrollView>

      {/* Footer Nav */}
      <View style={styles.footer}>
        <TouchableOpacity style={styles.navItem}>
          <TrendingUp color="#58A6FF" size={24} />
          <Text style={[styles.navText, { color: "#58A6FF" }]}>Markets</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Globe color="#8B949E" size={24} />
          <Text style={styles.navText}>Global</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#010409',
  },
  header: {
    padding: 24,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#161B22',
  },
  headerLabel: {
    color: '#8B949E',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 2,
  },
  headerTitle: {
    color: '#F0F6FC',
    fontSize: 24,
    fontWeight: '700',
  },
  content: {
    flex: 1,
  },
  chartContainer: {
    margin: 20,
    backgroundColor: '#0D1117',
    borderRadius: 12,
    padding: 20,
    borderWidth: 1,
    borderBottomColor: '#30363D',
  },
  chartHeader: {
    marginBottom: 20,
  },
  chartTitle: {
    color: '#8B949E',
    fontSize: 14,
    fontWeight: '600',
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
  },
  priceText: {
    color: '#F0F6FC',
    fontSize: 32,
    fontWeight: '700',
    marginRight: 12,
  },
  changeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  changeText: {
    fontSize: 12,
    fontWeight: '700',
  },
  listSection: {
    padding: 20,
  },
  sectionTitle: {
    color: '#F0F6FC',
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 16,
  },
  card: {
    backgroundColor: '#161B22',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#30363D',
  },
  activeCard: {
    borderColor: '#58A6FF',
    backgroundColor: '#1F242C',
  },
  cardCategory: {
    color: '#8B949E',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
  },
  cardName: {
    color: '#F0F6FC',
    fontSize: 16,
    fontWeight: '600',
  },
  footer: {
    height: 80,
    backgroundColor: '#0D1117',
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#30363D',
  },
  navItem: {
    alignItems: 'center',
  },
  navText: {
    color: '#8B949E',
    fontSize: 10,
    marginTop: 4,
    fontWeight: '600',
  },
  errorText: {
    color: '#F85149',
    textAlign: 'center',
    padding: 20,
  }
});
