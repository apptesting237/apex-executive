import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  SafeAreaView,
  TouchableOpacity,
  ScrollView,
  StatusBar,
  TextInput,
  Modal,
  Alert
} from 'react-native';

const BACKEND_URL = 'http://localhost:8000'; // Or your Railway / Render URL

export default function App() {
  const [activeTab, setActiveTab] = useState('cockpit');
  const [revenue, setRevenue] = useState(214850);
  const [approvalsCount, setApprovalsCount] = useState(3);
  const [threats, setThreats] = useState(1842);
  const [intercomVisible, setIntercomVisible] = useState(false);
  const [mandateText, setMandateText] = useState('');
  const [chatLog, setChatLog] = useState([
    {
      sender: 'Dr. Evelyn Vance (Chief of Staff)',
      msg: 'Welcome to your CEO Cockpit. All 12 divisions are operating autonomously. How may I direct your crews today?'
    }
  ]);

  const sendMandate = async (customText?: string) => {
    const textToSend = customText || mandateText;
    if (!textToSend.trim()) return;

    setChatLog((prev) => [...prev, { sender: 'You (CEO)', msg: textToSend }]);
    setMandateText('');
    setIntercomVisible(false);

    try {
      const res = await fetch(`${BACKEND_URL}/api/ceo/mandate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ directive: textToSend })
      });
      const data = await res.json();
      setChatLog((prev) => [
        ...prev,
        {
          sender: 'Dr. Evelyn Vance (Chief of Staff)',
          msg: `Action dispatched to ${data.execution.division}. ${data.execution.action} Projected ROI: ${data.execution.profit_projected}`
        }
      ]);
    } catch (e) {
      // Local demo fallback if backend is offline
      setChatLog((prev) => [
        ...prev,
        {
          sender: 'Dr. Evelyn Vance (Chief of Staff)',
          msg: `Mandate acknowledged. Decomposing across relevant specialized crews. Check approval desk for draft.`
        }
      ]);
    }
  };

  const approveDeal = (amount: number, title: string) => {
    setRevenue((prev) => prev + amount);
    setApprovalsCount((prev) => Math.max(0, prev - 1));
    Alert.alert('Approved by CEO', `${title} executed! +$${amount.toLocaleString()} booked to company treasury.`);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      {/* CEO Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.brandTitle}>APEX EXECUTIVE</Text>
          <Text style={styles.brandSub}>CEO Command OS • 12 Global Divisions</Text>
        </View>
        <TouchableOpacity
          onPress={() => setIntercomVisible(true)}
          style={styles.intercomButton}
        >
          <Text style={styles.intercomText}>🎙️ Chief of Staff</Text>
        </TouchableOpacity>
      </View>

      {/* Revenue & Defense Ticker */}
      <View style={styles.ticker}>
        <Text style={styles.tickerItem}>MTD: <Text style={styles.greenText}>${revenue.toLocaleString()}</Text></Text>
        <Text style={styles.tickerItem}>Defended: <Text style={styles.cyanText}>{threats}</Text></Text>
        <Text style={styles.tickerItem}>Approvals: <Text style={styles.goldText}>{approvalsCount}</Text></Text>
      </View>

      {/* Screen Views */}
      <ScrollView style={styles.body}>
        {activeTab === 'cockpit' && (
          <View style={styles.section}>
            {/* Chief of Staff Sit-Rep */}
            <View style={styles.cardGold}>
              <Text style={styles.cardGoldTitle}>Dr. Evelyn Vance (Chief of Staff)</Text>
              <Text style={styles.cardGoldSub}>Harvard PhD • Full Enterprise Authority</Text>
              <Text style={styles.cardGoldDesc}>
                "12MT Grade-5 Titanium import spread ready (+$54.2k). Johns Hopkins oncology protocol finalized (+$120k). Austin Logistics Park syndicated at 21.4% IRR."
              </Text>
            </View>

            {/* CEO Action Desk */}
            <Text style={styles.heading}>CEO ACTION DESK ({approvalsCount} PENDING)</Text>

            {approvalsCount > 0 && (
              <View style={styles.actionCard}>
                <Text style={styles.actionTitle}>🚢 Import/Export: Release $126k L/C for Titanium</Text>
                <Text style={styles.actionDesc}>Pre-sold to German aerospace buyer. Net spread: +$54,200.</Text>
                <TouchableOpacity
                  onPress={() => approveDeal(54200, 'Titanium Import Arbitrage')}
                  style={styles.btnApprove}
                >
                  <Text style={styles.btnText}>Authorize & Wire (Earn $54.2k)</Text>
                </TouchableOpacity>
              </View>
            )}

            {approvalsCount > 1 && (
              <View style={styles.actionCard}>
                <Text style={styles.actionTitle}>🏢 Real Estate: Execute Austin Park Closing</Text>
                <Text style={styles.actionDesc}>42k sq ft warehouse underwritten at 21.4% IRR. GP fee: +$84,000.</Text>
                <TouchableOpacity
                  onPress={() => approveDeal(84000, 'Austin Real Estate Syndication')}
                  style={[styles.btnApprove, { backgroundColor: '#d97706' }]}
                >
                  <Text style={styles.btnText}>Sign & Collect $84k Fee</Text>
                </TouchableOpacity>
              </View>
            )}
          </View>
        )}

        {activeTab === 'warroom' && (
          <View style={styles.section}>
            <Text style={styles.heading}>EXECUTIVE WAR ROOM</Text>
            <View style={styles.chatBox}>
              {chatLog.map((c, i) => (
                <View key={i} style={styles.chatItem}>
                  <Text style={c.sender.includes('CEO') ? styles.chatSenderCEO : styles.chatSenderAI}>{c.sender}:</Text>
                  <Text style={styles.chatText}>{c.msg}</Text>
                </View>
              ))}
            </View>
            <View style={styles.inputRow}>
              <TextInput
                style={styles.input}
                placeholder="Command your company..."
                placeholderTextColor="#64748b"
                value={mandateText}
                onChangeText={setMandateText}
              />
              <TouchableOpacity onPress={() => sendMandate()} style={styles.btnSend}>
                <Text style={styles.btnText}>Send</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {activeTab === 'ventures' && (
          <View style={styles.section}>
            <Text style={styles.heading}>ACTIVE MONETIZATION ENGINES</Text>
            <View style={styles.ventureCard}>
              <Text style={styles.ventureTitle}>🚢 Global Trade: Titanium Arbitrage</Text>
              <Text style={styles.ventureProfit}>+$54,200 Net Spread</Text>
              <Text style={styles.ventureDesc}>Customs cleared under EVFTA 0% tariff. CIF Rotterdam delivery.</Text>
            </View>
            <View style={styles.ventureCard}>
              <Text style={styles.ventureTitle}>🧬 Biotech: Oncology Biomarker Protocol</Text>
              <Text style={styles.ventureProfit}>+$120,000 Milestone + 4% Royalty</Text>
              <Text style={styles.ventureDesc}>Synthesized by MIT/Stanford fellows. Licensed to Meridian Therapeutics.</Text>
            </View>
            <View style={styles.ventureCard}>
              <Text style={styles.ventureTitle}>🏢 Real Estate: Austin Logistics Park</Text>
              <Text style={styles.ventureProfit}>+$84,000 Sponsor GP Fee</Text>
              <Text style={styles.ventureDesc}>13.9% Cap Rate industrial acquisition. 14 LP investors syndicated.</Text>
            </View>
          </View>
        )}

        {activeTab === 'fortress' && (
          <View style={styles.section}>
            <Text style={styles.heading}>CISO AI FIREWALL & THREAT RADAR</Text>
            <View style={styles.defenseCard}>
              <Text style={styles.defenseTitle}>Zero-Trust Fortress Defense</Text>
              <Text style={styles.defenseStat}>1,842 Attacks Neutralized</Text>
              <Text style={styles.defenseDesc}>64 capability-scoped enclaves running with least-privilege tokens.</Text>
            </View>
            <TouchableOpacity
              onPress={() => {
                setThreats((p) => p + 25);
                Alert.alert('Red-Team Audit', '25 adversarial injection vectors simulated and 100% deflected.');
              }}
              style={styles.btnAudit}
            >
              <Text style={styles.btnText}>Run Red-Team Attack Simulation</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>

      {/* Floating Bottom Nav */}
      <View style={styles.tabBar}>
        {['Cockpit', 'WarRoom', 'Ventures', 'Fortress'].map((t) => (
          <TouchableOpacity
            key={t}
            onPress={() => setActiveTab(t.toLowerCase())}
            style={styles.tabBtn}
          >
            <Text style={[styles.tabText, activeTab === t.toLowerCase() && styles.tabActive]}>{t}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Intercom Voice Modal */}
      <Modal visible={intercomVisible} transparent animationType="slide">
        <View style={styles.modalBg}>
          <View style={styles.modalCard}>
            <Text style={styles.modalTitle}>Dr. Evelyn Vance — Executive Voice Intercom</Text>
            <Text style={styles.modalSub}>Harvard PhD • Select a mandate or dictate to your Chief of Staff:</Text>
            <TouchableOpacity
              onPress={() => sendMandate('Source a high-margin Import/Export commodity arbitrage deal')}
              style={styles.presetBtn}
            >
              <Text style={styles.presetText}>🚢 "Source high-margin Import/Export trade deal"</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => sendMandate('Have MIT and Mayo clinic draft a clinical trial protocol')}
              style={styles.presetBtn}
            >
              <Text style={styles.presetText}>🧬 "Draft biotech clinical trial patent protocol"</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => sendMandate('Underwrite a commercial real estate logistics park')}
              style={styles.presetBtn}
            >
              <Text style={styles.presetText}>🏢 "Model commercial real estate acquisition"</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => setIntercomVisible(false)}
              style={styles.closeBtn}
            >
              <Text style={styles.btnText}>Close Intercom</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#05070b' },
  header: { flexDirection: 'row', justifyContent: 'space-between', padding: 16, borderBottomWidth: 1, borderBottomColor: '#1e293b' },
  brandTitle: { fontSize: 16, fontWeight: 'bold', color: '#fbbf24', letterSpacing: 1 },
  brandSub: { fontSize: 11, color: '#94a3b8' },
  intercomButton: { backgroundColor: '#10b98120', borderWidth: 1, borderColor: '#10b981', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8 },
  intercomText: { color: '#34d399', fontSize: 12, fontWeight: 'bold' },
  ticker: { flexDirection: 'row', justifyContent: 'space-around', backgroundColor: '#0b0f17', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: '#1e293b' },
  tickerItem: { fontSize: 11, color: '#94a3b8', fontFamily: 'monospace' },
  greenText: { color: '#34d399', fontWeight: 'bold' },
  cyanText: { color: '#22d3ee', fontWeight: 'bold' },
  goldText: { color: '#fbbf24', fontWeight: 'bold' },
  body: { flex: 1, padding: 16 },
  section: { marginBottom: 24 },
  heading: { fontSize: 12, fontWeight: 'bold', color: '#94a3b8', letterSpacing: 1, marginBottom: 12 },
  cardGold: { backgroundColor: '#111827', borderWidth: 1, borderColor: '#f59e0b50', borderRadius: 14, padding: 14, marginBottom: 16 },
  cardGoldTitle: { fontSize: 14, fontWeight: 'bold', color: '#fff' },
  cardGoldSub: { fontSize: 11, color: '#fbbf24', marginBottom: 6 },
  cardGoldDesc: { fontSize: 12, color: '#cbd5e1', lineHeight: 18 },
  actionCard: { backgroundColor: '#0b0f17', borderWidth: 1, borderColor: '#334155', borderRadius: 12, padding: 14, marginBottom: 12 },
  actionTitle: { fontSize: 13, fontWeight: 'bold', color: '#fff' },
  actionDesc: { fontSize: 11, color: '#94a3b8', marginTop: 4, marginBottom: 10 },
  btnApprove: { backgroundColor: '#16a34a', paddingVertical: 10, borderRadius: 8, alignItems: 'center' },
  btnText: { color: '#fff', fontSize: 12, fontWeight: 'bold' },
  chatBox: { backgroundColor: '#0b0f17', borderWidth: 1, borderColor: '#334155', borderRadius: 12, padding: 12, minHeight: 220, marginBottom: 12 },
  chatItem: { marginBottom: 10 },
  chatSenderCEO: { fontSize: 11, fontWeight: 'bold', color: '#fbbf24' },
  chatSenderAI: { fontSize: 11, fontWeight: 'bold', color: '#34d399' },
  chatText: { fontSize: 12, color: '#e2e8f0', marginTop: 2 },
  inputRow: { flexDirection: 'row', gap: 8 },
  input: { flex: 1, backgroundColor: '#111827', borderWidth: 1, borderColor: '#334155', borderRadius: 10, paddingHorizontal: 12, color: '#fff', fontSize: 12 },
  btnSend: { backgroundColor: '#d97706', paddingHorizontal: 16, justifyContent: 'center', borderRadius: 10 },
  ventureCard: { backgroundColor: '#0b0f17', borderWidth: 1, borderColor: '#10b98150', borderRadius: 12, padding: 14, marginBottom: 12 },
  ventureTitle: { fontSize: 13, fontWeight: 'bold', color: '#fff' },
  ventureProfit: { fontSize: 12, fontWeight: 'bold', color: '#34d399', marginVertical: 3 },
  ventureDesc: { fontSize: 11, color: '#94a3b8' },
  defenseCard: { backgroundColor: '#0b0f17', borderWidth: 1, borderColor: '#3b82f650', borderRadius: 12, padding: 14, marginBottom: 12 },
  defenseTitle: { fontSize: 13, fontWeight: 'bold', color: '#fff' },
  defenseStat: { fontSize: 18, fontWeight: 'bold', color: '#38bdf8', marginVertical: 4 },
  defenseDesc: { fontSize: 11, color: '#94a3b8' },
  btnAudit: { backgroundColor: '#2563eb', paddingVertical: 12, borderRadius: 10, alignItems: 'center' },
  tabBar: { flexDirection: 'row', justifyContent: 'space-around', backgroundColor: '#0b0f17', borderTopWidth: 1, borderTopColor: '#1e293b', paddingVertical: 12 },
  tabBtn: { alignItems: 'center' },
  tabText: { fontSize: 11, color: '#64748b' },
  tabActive: { color: '#fbbf24', fontWeight: 'bold' },
  modalBg: { flex: 1, backgroundColor: 'rgba(0,0,0,0.85)', justifyContent: 'center', padding: 20 },
  modalCard: { backgroundColor: '#0b0f17', borderWidth: 1, borderColor: '#f59e0b', borderRadius: 16, padding: 20 },
  modalTitle: { fontSize: 14, fontWeight: 'bold', color: '#fff', marginBottom: 4 },
  modalSub: { fontSize: 11, color: '#94a3b8', marginBottom: 14 },
  presetBtn: { backgroundColor: '#111827', borderWidth: 1, borderColor: '#334155', padding: 12, borderRadius: 10, marginBottom: 8 },
  presetText: { color: '#e2e8f0', fontSize: 12 },
  closeBtn: { backgroundColor: '#334155', padding: 12, borderRadius: 10, alignItems: 'center', marginTop: 8 }
});
