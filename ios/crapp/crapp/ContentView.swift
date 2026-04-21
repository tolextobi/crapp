import SwiftUI
import Combine

struct ContentView: View {
    @State private var minutesSince: Double? = nil
    @State private var alertThreshold: Double = 60
    @State private var timer = Timer.publish(every: 30, on: .main, in: .common).autoconnect()

    var minutesLeft: Double? {
        guard let since = minutesSince else { return nil }
        return max(0, alertThreshold - since)
    }

    var body: some View {
        ZStack {
            Color(.systemGroupedBackground)
                .ignoresSafeArea()

            VStack(spacing: 48) {
                VStack(spacing: 8) {
                    Text("CRApp")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    Text("Check-in System")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }

                if let left = minutesLeft {
                    VStack(spacing: 6) {
                        Text("Nächster Check-in in")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        Text("\(Int(left)) Minuten")
                            .font(.system(size: 48, weight: .semibold, design: .rounded))
                            .foregroundColor(left < 10 ? .red : .primary)
                    }
                    .padding(24)
                    .frame(maxWidth: .infinity)
                    .background(Color(.secondarySystemGroupedBackground))
                    .cornerRadius(20)
                    .padding(.horizontal)
                }

                Button(action: sendPing) {
                    Label("Alles gut", systemImage: "heart.fill")
                        .font(.title2)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 20)
                        .background(Color.pink)
                        .cornerRadius(16)
                        .padding(.horizontal)
                }
            }
        }
        .onAppear { fetchStatus() }
        .onReceive(timer) { _ in fetchStatus() }
    }

    func sendPing() {
        guard let url = URL(string: "http://192.168.0.35:8000/ping") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        URLSession.shared.dataTask(with: request) { _, _, _ in
            fetchStatus()
        }.resume()
    }

    func fetchStatus() {
        guard let url = URL(string: "http://192.168.0.35:8000/status") else { return }
        URLSession.shared.dataTask(with: url) { data, _, _ in
            guard let data = data,
                  let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                  let minutes = json["minutes_since_ping"] as? Double,
                  let threshold = json["alert_threshold_minutes"] as? Double
            else { return }
            DispatchQueue.main.async {
                self.minutesSince = minutes
                self.alertThreshold = threshold
            }
        }.resume()
    }
}
